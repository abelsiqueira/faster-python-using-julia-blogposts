using DelimitedFiles

function load_confusjl(filename)
  file = read(filename)
  n = sum(c == UInt8(',') || c == UInt8('\n') for c in file) + 1
  if file[end] == UInt8('\n') # Pesky extra blank line
    n -= 1
  end
  c = Ref{Cchar}(0)
  # n = 0
  # f = ccall(:fopen, Ptr{Cvoid}, (Cstring, Cstring), filename, "r")
  # while ccall(:fscanf, Cint, (Ptr{Cvoid}, Cstring, Ref{Cchar}), f, "%c", c) > 0
  #   if c[] == Int8(',') || c == Int8('\n')
  #     n += 1
  #   end
  # end
  # ccall(:fclose, Ptr{Cvoid}, (Ptr{Cvoid},), f)
  keys = zeros(Int, n)
  indexes = zeros(Int, n)
  values = zeros(Int, n)

  x = Ref{Int}(0)
  count = 1
  k = -1
  j = 0
  f = ccall(:fopen, Ptr{Cvoid}, (Cstring, Cstring), filename, "r")
  while true
    ccall(:fscanf, Cint, (Ptr{Cvoid}, Cstring, Ref{Int}, Ref{Cchar}), f, "%ld%c", x, c)
    if c[] == Int8('#')
      k = x[]
      j = 0
    else
      keys[count] = k
      indexes[count] = j
      j += 1
      values[count] = x[]
      count += 1
    end
    count > n && break
  end
  ccall(:fclose, Ptr{Cvoid}, (Ptr{Cvoid},), f)

  return keys, indexes, values
end

# filename = "confus.txt"
# filename = "input_simple.txt"
# filename = "pandas_loading_benchmarks_data.txt"
# load_confusjl(filename)
# @time load_confusjl(filename);