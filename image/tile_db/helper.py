import tiledb

def get_dataset_count(tile_uri):
    with tiledb.open(tile_uri, 'r') as A:
        return len(A)

# if __name__ == "__main__":
#     print(get_dataset_count(tile_uri="/mnt/data/dataset/cifar/cifar100.tldb"))