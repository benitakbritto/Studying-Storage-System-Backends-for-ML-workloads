# CS744-Project

[Project Proposal](https://drive.google.com/drive/u/2/folders/17alBOquTtHBdmi9bu8b_zSJWVMvB24WF)
[Project Check-in](https://docs.google.com/document/d/1ZmUIVHlWYe_GlfWPdzbpVuOkVHCzkgGqR1IKiRh_7Cg/edit#)

### File Structure
Code: TODO 
Dataset: TODO

### Datasets
1. [Twitter Dataset](https://www.kaggle.com/datasets/kazanova/sentiment140)
2. [CIFAR-100](https://www.kaggle.com/datasets/fedesoriano/cifar100)
3. [FB15K-237](https://www.microsoft.com/en-us/download/details.aspx?id=52312), [Papers with Code](https://paperswithcode.com/dataset/fb15k-237)

Note: All datasets were stored under the path `/mnt/data/datasets`

### Modified Dataset
Concatenate the dataset for each ML workload to move a larger version of it (TODO: Add path to util)

### Installation
#### RocksDB
1. `cd /mnt/data`
2. `git clone https://github.com/facebook/rocksdb.git`
3. `cd rocksdb`
4. `DEBUG_LEVEL=0 make shared_lib install-shared`
5. `export LD_LIBRARY_PATH=/usr/local/lib`
6. `pip install rocksdb3` (More info on [rocksdb3](https://pypi.org/project/rocksdb3/)) OR
`pip install rocksdict` (More info on [RocksDict](https://github.com/Congyuwang/RocksDict))

#### TileDB
$ conda install numpy pandas

$ conda install -c conda-forge tiledb-py pyarrow

#### TensorStore
TODO

#### PyTorch
TODO

### Commands
TODO

### Metrics Ideas:
- READ: Time, Memory, CPU - Change prefetch size (for all ds)
- WRITE: Time, Memory, CPU - Change bulk insertion size (for all ds)

### TODO GRAPHS
- Increase batch size in dataloader and note elapsed time

## Experiments
The scripts are present in the `/scripts` dir. Prerequesite to running the scripts is to create the output directories using `/scripts/make_output_folders.sh`. The results for the tests will be stored here.  

We test the performance across different ML (text, image, graph) workloads on input data (using map and iterable style dataloaders) and intermediate data (embeddings). We further tune the follwing parameters: 

### Parameters: Map style dataloader
- input file size
- number of workers (only for TileDB, TensorStore)
- batch size
- number of input rows per key (only for RocksDB)

### Parameters: Iterable style dataloader
- input file size
- number of workers (only for TileDB, TensorStore)
- batch size
- prefetch size

### Parameters: Intermediate data
TODO

### Workloads
#### Text
`1. Concatenate input dataset`  
`2. Run map style script from /scripts/text/map_style.sh`  
`3. Run iterable style script from /scripts/text/iterable_style.sh`  

#### Image
`1. Concatenate input dataset`  
`2. Run map style script from /scripts/text/map_style.sh`  
`3. Run iterable style script from /scripts/text/iterable_style.sh`  

#### Graph
`1. Concatenate input dataset`  
`2. Run map style script from /scripts/text/map_style.sh`  
`3. Run iterable style script from /scripts/text/iterable_style.sh`  

#### Embedding
TODO
