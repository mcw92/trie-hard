import multiprocessing


def check_start_with_prefix(prefix, string_list):
    return [s for s in string_list if s.startswith(prefix)]


if __name__ == "__main__":
    prefix = "example"
    string_list = ["example123", "example456", "test789", "example789"]

    # Create a process pool with the number of CPU cores available
    pool = multiprocessing.Pool(processes=2)

    # Split the string_list into chunks for parallel processing
    chunk_size = len(string_list) // 2
    chunks = [string_list[i:i + chunk_size] for i in range(0, len(string_list), chunk_size)]

    # Use the pool.map() function to apply the function to each chunk in parallel
    results = pool.map(check_start_with_prefix, [(prefix, chunk) for chunk in chunks])

    # Flatten the results list
    flattened_results = [item for sublist in results for item in sublist]

    pool.close()
    pool.join()

    print(flattened_results)
