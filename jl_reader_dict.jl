using Parsers

function read_arrays_jl_dict(filename)
  lines = split.(readlines(filename), "#")
  D = Dict(
    Parsers.parse(Int, line[1]) => Parsers.parse.(Int, split(line[2], ","))
    for line in lines
  )
  n = sum(length(v) for (k, v) in D)
  keys = zeros(Int, n)
  indexes = zeros(Int, n)
  values = zeros(Int, n)

  count = 0
  for (k, v) in D
    m = length(v)
    idx = count+1:count+m
    keys[idx] .= k
    indexes[idx] .= 0:m-1
    values[idx] .= v
    count += m
  end

  return keys, indexes, values
end

# filename = "confus.txt"
# filename = "input_simple.txt"
# filename = "pandas_loading_benchmarks_data.txt"
# filename = "gen-data/confus-001-0.txt"
# load_confus_dict(filename)
# @time load_confus_dict(filename);