export interface SortIdItem {
  id: number;
  sortIndex: number;
}

export const sortBySortIndexAndGetSortedIds = (
  array: SortIdItem[],
): number[] => {
  const sortedArray = array.slice().sort((a, b) => a.sortIndex - b.sortIndex);
  const sortedIds = sortedArray.map((item) => item.id);
  return sortedIds;
};

export const rebuildSortIndex = (array: SortIdItem[]) => {
  array.forEach((item: SortIdItem, index: number) => {
    item.sortIndex = index; // 更新 sortIndex 为当前索引值
  });
};

export const removeSortItemById = (
  array: SortIdItem[],
  idToRemove: number,
): SortIdItem[] => {
  return array.filter((item) => item.id !== idToRemove);
};
