# CS744-Project

[Project Proposal](https://drive.google.com/drive/u/2/folders/17alBOquTtHBdmi9bu8b_zSJWVMvB24WF)

### Datasets
1. [Twitter Dataset](https://www.kaggle.com/datasets/kazanova/sentiment140)
2. [ImageNet Dataset](https://image-net.org/download-images.php)
3. [CIFAR-100](https://www.kaggle.com/datasets/fedesoriano/cifar100)
4. [FB15K-237](https://www.microsoft.com/en-us/download/details.aspx?id=52312)
5. [FB15K Large](https://developers.google.com/freebase) -- this is too big

### Installation

#### RocksDB
1. `cd /mnt/data`
2. `git clone https://github.com/facebook/rocksdb.git`
3. `cd rocksdb`
4. `DEBUG_LEVEL=0 make shared_lib install-shared`
5. `export LD_LIBRARY_PATH=/usr/local/lib`
6. `pip install rocksdb3` (More info on [rocksdb3](https://pypi.org/project/rocksdb3/)

#### TileDB
$ conda install numpy pandas

$ conda install -c conda-forge tiledb-py pyarrow

#### TensorStore
TODO

#### PyTorch
TODO

### File Structure
- Twitter dataset: /mnt/data/twitter/

## Metrics Ideas:
- READ: Time, Memory, CPU - Change prefetch size (for all ds)
- WRITE: Time, Memory, CPU - Change bulk insertion size (for all ds)

## TODO GRAPHS
- Increase batch size in dataloader and note elapsed time
