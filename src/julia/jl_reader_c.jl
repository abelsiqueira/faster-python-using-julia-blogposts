using DelimitedFiles

function read_arrays_jl_c(filename)
  fmt = "%ld%c"
  c = Ref{Cchar}(0)
  x = Ref{Int}(0)
  n = 0
  set = UInt8[',', '#']
  f = ccall(:fopen, Ptr{Cvoid}, (Cstring, Cstring), filename, "r")
  while ccall(:fscanf, Cint, (Ptr{Cvoid}, Cstring, Ref{Int}, Ref{Cchar}), f, fmt, x, c) == 2
    if c[] in set
      n += 1
    end
  end
  ccall(:fclose, Ptr{Cvoid}, (Ptr{Cvoid},), f)

  keys = zeros(Int, n)
  indexes = zeros(Int, n)
  elements = zeros(Int, n)

  count = 1
  k = -1
  j = 0
  f = ccall(:fopen, Ptr{Cvoid}, (Cstring, Cstring), filename, "r")
  while ccall(:fscanf, Cint, (Ptr{Cvoid}, Cstring, Ref{Int}, Ref{Cchar}), f, fmt, x, c) == 2
    if c[] == Int8('#')
      k = x[]
      j = 0
    else
      keys[count] = k
      indexes[count] = j
      j += 1
      elements[count] = x[]
      count += 1
    end
  end
  ccall(:fclose, Ptr{Cvoid}, (Ptr{Cvoid},), f)

  return keys, indexes, elements
end