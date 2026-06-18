// https://github.com/samicpp/sorting-algorithms/blob/main/rust_sort/src/sort/heap.rs

fn number_heapify(arr: &mut Vec<(String, i64)>, n: usize, i: usize) -> ()
{
    let mut max = i;
    let left = 2 * i + 1;
    let right = 2 * i + 2;

    if left < n && arr[left].1 > arr[max].1 {
        max = left;
    }
    if right < n && arr[right].1 > arr[max].1 {
        max = right;
    }
    if max != i {
        arr.swap(i, max);
        number_heapify(arr, n, max);
    }
}

pub fn number(mut arr: Vec<(String, i64)>) -> Vec<(String, i64)>
{
    let len = arr.len();
    let mut i = len / 2;
    while i > 0 {
        i -= 1;
        number_heapify(&mut arr, len, i);
    }
    let mut i = len;
    while i > 0 {
        i -= 1;
        arr.swap(0, i);
        number_heapify(&mut arr, i, 0);
    }

    arr
}
