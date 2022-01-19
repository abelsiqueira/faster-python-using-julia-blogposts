using CSV, DataFrames, Printf, Random

include("gen_confus.jl")

function gen_dataset(seed = 123, folder="dataset")
  info_filenames = String[]
  info_rows = Int[]
  info_elems = Int[]
  count = 0
  if isdir(folder)
    error("dataset folder exists. Remove it")
  else
    mkdir(folder)
  end
  Random.seed!(seed)
  for col_max = round.(Int, 10 .^ (0.5:0.5:4.5))
    for n_rows = 50:50:500
      for dense in [true, false]
        cm = dense ? col_max : 10col_max
        count += 1
        filename = @sprintf("dataset/file-%04d.txt", count)
        n_elem = gen_confus(filename=filename, n_rows=n_rows, col_max=cm, dense=dense)
        println("$count rows=$n_rows n_elem=$n_elem cm=$cm dense=$dense")
        push!(info_filenames, filename)
        push!(info_rows, n_rows)
        push!(info_elems, n_elem)
      end
    end
  end

  DataFrame(:filename => info_filenames, :nrows => info_rows, :nelements => info_elems) |> CSV.write("dataset/info.csv")
end