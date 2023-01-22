use fraction::BigFraction;
use pyo3::prelude::*;
use std::time::{SystemTime, UNIX_EPOCH};

mod data;
mod algorithm;


/// Performs LLL basis reduction.
#[pyfunction]
fn reduce(file_name: String) -> PyResult<String> {
    let input = data::read(file_name);
    let start = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis();
    let basis = algorithm::reduce(input, BigFraction::from(0.75));
    let finish = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis();
    println!("{}", finish - start);
    Ok(basis.len().to_string())
}

#[pymodule]
fn lll_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(reduce, m)?)?;
    Ok(())
}