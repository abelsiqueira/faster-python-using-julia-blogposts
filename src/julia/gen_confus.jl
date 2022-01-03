function gen_confus(;
  filename = "confus.txt",
  n_rows = 50,
  col_max = 5000,
)
  keys = sort(rand(100_000:999_999, n_rows))
  while !allunique(keys)
    keys = unique(keys)
    keys = [keys; rand(1:100_000, n_rows - length(keys))]
  end
  open(filename, "w") do io
    for i = 1:n_rows
      n_cols = round(Int, exp(rand(0:0.1:log(col_max))))
      cols = sort(rand(100_000:999_999, n_cols))
      line = string(keys[i]) * "#" * join(cols, ",")
      println(io, line)
    end
  end
end