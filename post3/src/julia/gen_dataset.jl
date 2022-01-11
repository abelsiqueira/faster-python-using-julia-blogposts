using CSV, DataFrames, Printf, Random

include("gen_confus.jl")

function gen_dataset(seed = 123)
  info_filenames = String[]
  info_rows = Int[]
  info_elems = Int[]
  count = 0
  isdir("dataset") || mkdir("dataset")
  Random.seed!(seed)
  for col_max = round.(Int, 10 .^ (2:0.5:5))
    for n_rows = 100:100:500
      count += 1
      filename = @sprintf("dataset/file-%04d.txt", count)
      n_elem = gen_confus(filename=filename, n_rows=n_rows, col_max=col_max)
      println("$count rows=$n_rows n_elem=$n_elem")
      push!(info_filenames, filename)
      push!(info_rows, n_rows)
      push!(info_elems, n_elem)
    end
  end

  DataFrame(:filename => info_filenames, :nrows => info_rows, :nelements => info_elems) |> CSV.write("dataset/info.csv")
end

gen_dataset()