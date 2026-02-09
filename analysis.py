from scripts import sort_data, plot_data, summarize

print("Preparing data...")
sort_data.main()

print("Generating graphs...")
plot_data.main()

print("Generating summaries...")
summarize.main()

print("Analysis successful!")