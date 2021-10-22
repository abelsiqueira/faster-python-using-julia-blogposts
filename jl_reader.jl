using DelimitedFiles

function load_confusjl(filename)
  file = read(filename)
  n = sum(c == UInt8(',') || c == UInt8('\n') for c in file) + 1
  replace!(file, UInt8('#') => UInt8(','))
  keys = zeros(Int, n)
  indexes = zeros(Int, n)
  values = zeros(Int, n)
  line_breaks = [0; findall(file .== UInt8('\n')); length(file)+1]
  n_brks = length(line_breaks)
  i = 1
  for ln = 1:n_brks-1
    @views V = readdlm(IOBuffer(file[line_breaks[ln]+1:line_breaks[ln+1]-1]), ',', Int)
    k = V[1]
    for (j, v) in enumerate(@view V[2:end])
      keys[i] = k
      indexes[i] = j - 1
      values[i] = v
      i += 1
    end
  end

  return keys, indexes, values
end

filename = "confus.txt"
@time load_confusjl(filename);