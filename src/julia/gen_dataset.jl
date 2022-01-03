using Printf

include("gen_confus.jl")

count = 1
isdir("dataset") || mkdir("dataset")
for col_max = round.(10 .^ (3:0.5:6), sigdigits=1)
  for n_rows = 25:25:500
    println("$count $n_rows $col_max")
    filename = @sprintf("dataset/file-%04d.txt", count)
    gen_confus(filename=filename, n_rows=n_rows, col_max=col_max)
    count += 1
  end
end