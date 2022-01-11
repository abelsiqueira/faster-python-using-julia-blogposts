function read_arrays_jl_basic(filename)
  keys = Int[]
  indexes = Int[]
  elements = Int[]
  for line in readlines(filename)
    s = split(line, "#")
    k, v = parse(Int, s[1]), parse.(Int, split(s[2], ","))
    m = length(v)
    keys = [keys; fill(k, m)]
    indexes = [indexes; 0:m-1]
    elements = [elements; v]
  end

  return keys, indexes, elements
end