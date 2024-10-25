#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Return a dictionary with pagination info and data, handling deleted indices.
        
        Args:
            index: Starting index for pagination
            page_size: Number of records per page
            
        Returns:
            Dict containing:
            - index: Current start index
            - next_index: Next index to query
            - page_size: Size of page
            - data: List of actual data
        """
        # Validate inputs
        assert isinstance(index, int) and index is not None
        assert isinstance(page_size, int) and page_size > 0
        dataset = self.indexed_dataset()
        dataset_size = len(dataset)
        assert 0 <= index < dataset_size

        data = []
        next_index = index
        # Keep collecting data until we have page_size items
        while len(data) < page_size and next_index < dataset_size:
            if next_index in dataset:
                data.append(dataset[next_index])
            next_index += 1

        return {
            'index': index,
            'next_index': next_index,
            'page_size': page_size,
            'data': data
        }