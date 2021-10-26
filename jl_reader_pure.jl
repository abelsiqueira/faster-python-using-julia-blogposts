using DelimitedFiles, Parsers

function load_confus_purejl(filename)
  file = read(filename)
  n = sum(c == UInt8(',') || c == UInt8('\n') for c in file) + 1
  if file[end] == UInt8('\n') # Pesky extra blank line
    n -= 1
  end
  keys = zeros(Int, n)
  indexes = zeros(Int, n)
  values = zeros(Int, n)

  count = 1
  k = -1
  j = 0
  fi = 1
  fj = 2
  fn = length(file)
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
      values[count] = x
      count += 1
    end
    fi = fj + 1
    fj = fi + 1
  end

  return keys, indexes, values
end

# filename = "confus.txt"
# filename = "input_simple.txt"
# filename = "pandas_loading_benchmarks_data.txt"
# load_confus_purejl(filename)
# @time load_confus_purejl(filename);