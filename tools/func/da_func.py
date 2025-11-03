def get_runtime_data(runtime_result: list[int]) -> None:
    print(f"Min runtime: {min(runtime_result)}\n"
          f"Max runtime: {max(runtime_result)}\n"
          f"Avg runtime: {sum(runtime_result) / len(runtime_result)}")
    # print(runtime_result)