# Helper function to count the number occurences of a key
def count_key_occurrences(json_data, target_key):
    def recursive_count(data, target_key):
        count = 0
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    count += 1
                count += recursive_count(value, target_key)
        elif isinstance(data, list):
            for item in data:
                count += recursive_count(item, target_key)
        return count

    return recursive_count(json_data, target_key)