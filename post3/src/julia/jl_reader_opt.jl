using Parsers

function read_arrays_jl_opt(filename)
  file = read(filename)
  n = sum(c == UInt8(',') || c == UInt8('#') for c in file)
  keys = zeros(Int, n)
  indexes = zeros(Int, n)
  elements = zeros(Int, n)

  count, k, j, fi, fj, fn = 1, -1, 0, 1, 2, length(file)

  while fi < fn && count ≤ n
    while (file[fj] ≥ 0x30) fj += 1 end
    x = Parsers.parse(Int, view(file, fi:fj-1))
    c = file[fj]
    if c == Int8('#')
      k = x
      j = 0
    else
      keys[count] = k
      indexes[count] = j
      j += 1
      elements[count] = x
      count += 1
    end
    fi = fj + 1
    fj = fi + 1
  end

  return keys, indexes, elements
end