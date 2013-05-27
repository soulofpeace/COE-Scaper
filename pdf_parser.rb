require 'rubygems'
require 'bundler/setup'
require 'pdf-reader'
require 'date'
require 'json'

def parse_coe(lines, current_index, date, map)
  def parse_line(l, type, map, date)
    tokens = l.split()
    tokens[2..-1].each_with_index do |token, index|
      if index % 2 == 0
        category = case index
                   when 0
                     "A"
                   when 2
                     "B"
                   when 4
                     "C"
                   when 6
                     "D"
                   when 8
                     "E"
                   end
        date_first_bid = DateTime.new(date.year, date.month, 1, 0, 0, 0, 0)
        date_second_bid = DateTime.new(date.year, date.month, 15, 0, 0, 0, 0)
        map[category] ||= {} 
        map[category][date_first_bid] ||= {}
        map[category][date_first_bid][type] ||= {}
        map[category][date_first_bid][type] = token
        map[category][date_second_bid]||={}
        map[category][date_second_bid][type] ||= {}
        map[category][date_second_bid][type] = tokens[index+3]
      end
    end
  end

  count = 0 
  offset = 0 
  while count < 4
    if !lines[current_index+offset].nil? && lines[current_index+offset].strip != '' && lines[current_index+offset].strip.split.size >= 8
      type = case count
             when 0
               'quota'
             when 1
               'successful'
             when 2
               'received'
             when 3
               'premium'
             end

      parse_line(lines[current_index+offset], type , map, date)
      count = count + 1
    end
    offset = offset + 1
  end
  puts "map : #{JSON.pretty_generate(map)}"
  map
end

def initialize_coe_map 
  if File.exists? 'coe.json'
    raw_coe_map = File.read('coe.json')
    JSON.parse(raw_coe_map)
  else
    {}
  end
end

inputfile = ARGV[0]
map = initialize_coe_map


File.open(inputfile, "rb") do |f|
  reader = PDF::Reader.new(f)
  reader.pages.each do |page|
    text = page.text
    lines = text.lines.map(&:chomp)
    lines.each_with_index do |line, index|
      begin 
        line = line.strip
        puts "#{index} -> #{line}"
        date_string = line.split[0]
        if (!date_string.nil?) and !(date_string=~/month/i) and date_string =~ /[\w]{3}-[\d]{4}/ and (!date_string.include?(")"))
          date = DateTime.parse(date_string)
          puts "Date: #{date}"
          if date > DateTime.parse("Apr 2002") 
            parse_coe(lines, index, date, map)
            File.open('coe.json', 'w') do |file|
              file.write(map.to_json)
            end
          end
        end
      rescue ArgumentError  => e
        #puts e.inspect
      end
    end
  end
end




