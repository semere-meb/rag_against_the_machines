from src.indexer import Indexer

if __name__ == "__main__":
    indexer = Indexer()
    paths = indexer.get_all_paths()
    paths = indexer.filter_paths(paths)
    file_list = indexer.build_file_list(paths)
    print(len(file_list))
