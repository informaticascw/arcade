#[unsafe(no_mangle)]
pub extern "C" fn hello() {
    println!("Hello, world!");
}

mod heapsort;

#[pyo3::pymodule]
pub mod pijthon_psel_ffi {
    use pyo3::pyfunction;
    use crate::heapsort;



    #[pyfunction]
    pub fn test() {
        println!("hallo wereld wereld de wereld is van jou");
    }

    #[pyfunction]
    pub fn add_i64(x: i64, y: i64) -> i64 {
        x + y
    }

    #[pyfunction]
    pub fn panic(msg: Option<&str>) {
        if let Some(msg) = msg {
            panic!("{msg}")
        }
        else {
            panic!()
        }
    }

    
    #[pyfunction]
    pub fn sort_tuple_str_int(arr: Vec<(String, i64)>) -> Vec<(String, i64)> {
        heapsort::number(arr)
    }
    #[pyfunction]
    pub fn reverse_sort_tuple_str_int(arr: Vec<(String, i64)>) -> Vec<(String, i64)> {
        let mut a = heapsort::number(arr);
        a.reverse();
        a
    }
}
