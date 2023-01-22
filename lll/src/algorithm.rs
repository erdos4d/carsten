use std::ops::Div;
use fraction::{BigFraction, One, Zero};

fn dot(a: &Vec<BigFraction>, b: &Vec<BigFraction>) -> BigFraction {
    assert_eq!(a.len(), b.len());
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}

fn mu_square(mu: &[Vec<BigFraction>], k: usize) -> BigFraction {
    mu[k][k - 1].clone() * mu[k][k - 1].clone()
}

pub fn reduce(input: Vec<Vec<BigFraction>>, delta: BigFraction) -> Vec<Vec<BigFraction>> {
    assert!(delta >= BigFraction::from(0.25));
    assert!(delta <= BigFraction::from(1.0));
    let m = input.len();
    let n = input[0].len();
    let mut k = 1_usize;
    let mut y = input;
    let mut g_star: Vec<BigFraction> = Vec::new();
    let mut y_star: Vec<Vec<BigFraction>> = y;
    let mut mu: Vec<Vec<BigFraction>> = Vec::new();
    for i in 0..m {
        mu.push((0..m).map(
            |j|
                if j < i {
                    dot(&y[i], &y_star[j]).div(g_star[j])
                } else {
                    BigFraction::zero()
                }
        ).collect::<Vec<BigFraction>>());
        for j in 0..i {
            let temp_y = y_star[j].clone();
            let temp_mu = mu[i][j].clone();
            for l in 0..n {
                y_star[i][l] -= temp_mu.clone() * temp_y[l].clone();
            }
        }
        g_star.push(dot(&y_star[i], &y_star[i]));
    }
    while k < m {
        if mu[k][k - 1].abs() > BigFraction::from(0.5) {
            let r = mu[k][k - 1].clone().round();
            let temp = y[k - 1].clone();
            for l in 0..n {
                y[k][l] -= r.clone() * temp[l].clone();
            }
            for j in 0..k - 1 {
                let temp = mu[k - 1][j].clone();
                mu[k][j] -= r.clone() * temp.clone();
            }
            mu[k][k - 1] -= r.clone();
        }
        if g_star[k] >= (&delta - mu_square(&mu, k)) * g_star[k - 1].clone() {
            for l in (0..k - 1).rev() {
                if mu[k][l].abs() > BigFraction::from(0.5) {
                    let r = mu[k][l].clone().round();
                    let temp = y[l].clone();
                    for e in 0..n {
                        y[k][e] -= r.clone() * temp[e].clone();
                    }
                    for j in 0..l {
                        let temp = mu[l].clone();
                        mu[k][j] -= &r * temp[j].clone();
                    }
                    mu[k][l] -= &r;
                }
            }
            k += 1;
        } else {
            let nu = mu[k][k - 1].clone();
            let alpha = g_star[k].clone() + nu.clone() * nu.clone() * g_star[k - 1].clone();
            let g_temp = g_star[k - 1].clone();
            mu[k][k - 1] *= g_temp.clone() / alpha.clone();
            g_star[k] *= g_temp.clone() / alpha.clone();
            g_star[k - 1] = alpha.clone();
            let temp = y[k - 1].clone();
            y[k - 1] = y[k].clone();
            y[k] = temp;
            for j in 0..k - 1 {
                let temp = mu[k - 1][j].clone();
                mu[k - 1][j] = mu[k][j].clone();
                mu[k][j] = temp;
            }
            for i in k + 1..m {
                let xi = mu[i][k].clone();
                mu[i][k] = mu[i][k - 1].clone() - nu.clone() * mu[i][k].clone();
                mu[i][k - 1] = mu[k][k - 1].clone() * mu[i][k].clone() + xi.clone();
            }
            if k > 1 {
                k -= 1;
            }
        }
    }
    // hack to remove negative signs from zero terms
    y.iter().map(|vec| vec.iter().map(|int|
        if int.is_zero() && int.is_sign_negative() {
            int * BigFraction::from(-1)
        } else {
            int * BigFraction::one()
        }).collect::<Vec<BigFraction>>()).collect::<Vec<Vec<BigFraction>>>()
}

