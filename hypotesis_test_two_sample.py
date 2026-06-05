import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt


def get_t_table(alpha, tail, dof):  
    if tail == 2:
        alpha /= 2
    return st.t.isf([alpha], [dof]) [0]

def plot_critical_region(t_calc, t_table, dof, tail=1, direction="right"):
    """
    Fungsi untuk menggambar kurva t-distribution, daerah kritis (rejection region),
    dan posisi t_calc.
    """
    # Menentukan batas sumbu X agar grafik selalu mencakup t_calc dan t_table
    x_min = min(-4, t_calc - 1, -t_table - 1)
    x_max = max(4, t_calc + 1, t_table + 1)
    x = np.linspace(x_min, x_max, 1000)
    
    # Menghitung nilai Y berdasarkan t-distribution
    y = st.t.pdf(x, dof)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=f"t-distribution (df={dof})", color='black')

    # Mewarnai daerah kritis (Rejection Region)
    if tail == 2:
        # Two-Tailed
        x_left = x[x <= -t_table]
        plt.fill_between(x_left, st.t.pdf(x_left, dof), color='red', alpha=0.3, label='Rejection Region')
        
        x_right = x[x >= t_table]
        plt.fill_between(x_right, st.t.pdf(x_right, dof), color='red', alpha=0.3)
        
        plt.axvline(-t_table, color='red', linestyle='--', label=f'Critical -t ({--t_table:.2f})')
        plt.axvline(t_table, color='red', linestyle='--', label=f'Critical +t ({t_table:.2f})')
        
    elif tail == 1 and direction == "right":
        # One-Tailed (Right)
        x_right = x[x >= t_table]
        plt.fill_between(x_right, st.t.pdf(x_right, dof), color='red', alpha=0.3, label='Rejection Region')
        plt.axvline(t_table, color='red', linestyle='--', label=f'Critical t ({t_table:.2f})')
        
    elif tail == 1 and direction == "left":
        # One-Tailed (Left)
        x_left = x[x <= -t_table]
        plt.fill_between(x_left, st.t.pdf(x_left, dof), color='red', alpha=0.3, label='Rejection Region')
        plt.axvline(-t_table, color='red', linestyle='--', label=f'Critical -t ({-t_table:.2f})')

    # Menandai posisi t_calc (Hasil hitung sampel)
    plt.axvline(t_calc, color='blue', linestyle='-', linewidth=2, label=f't_calc ({t_calc:.2f})')

    # Merapikan tampilan grafik
    plt.title("Hypothesis Testing - Critical Region")
    plt.xlabel("t-value")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.show()

    
# hanya input bagian yang ditandai '<--'

vct_ds = "https://raw.githubusercontent.com/kolqz1/STATISTIC/refs/heads/main/dataset%20player%20vct%2025%20cleaned%20-%20player_stats_cleanedd%20(1).csv"
df = pd.read_csv(vct_ds)

# 1. Rata-rata ACS pemain sentinel sama dengan pemain controller.

# Step 1: State null and alternate hypotesis
# H0: μ Duelist <= μ Controller  <--
# H1: μ Duelist > μ Controller   <--

# Step 2: Select the level of significance
Sentinel = df[df['Role'] == 'Sentinel'] ['Average Combat Score']     # <-- ddf[df['Category_Collumn'] == 'Category 1'] ['Metrik_column'] dan ganti variabelnya
controller = df[df['Role'] == 'Controller'] ['Average Combat Score'] # <-- df[df['Category_Collumn'] == 'Category 2'] ['Metrik_column'] dan ganti variabelnya

alpha = 0.05    # Level of significance
tail = 2     # two-tailed

n_s = len(Sentinel)
n_c = len(controller)

Xbar_d = Sentinel.mean()
Xbar_c = controller.mean()

s2_s = Sentinel.var()
s2_c = controller.var()

dof = n_s + n_c - 2

s2P = ((n_s - 1) * s2_s + (n_c - 1) * s2_c) / dof

# Step 3: Determine the test statistic
# t-test with pooled variance because both standar deviation is unknown but both have the same value.

# Step 4: Formulate the decision rule
# Reject H0 if |t_calc| > t_table

# Step 5: Make the decision regarding H0
t_calc = (Xbar_d - Xbar_c) / np.sqrt(s2P * ((1 / n_s) + (1 / n_c)))
t_table = get_t_table(alpha, tail, dof)

print("t_calc = ", round(t_calc, 2))
print("t_table = ", round(t_table, 2))

# # Step 6: Interpret the result
if abs(t_calc) > t_table:
    print("H0 is rejected, the mean ACS of Sentinel player are not the same as Controller player")
else:
    print("H0 is fail to rejected, the mean ACS of Sentinel player are the same as Controller player")

plot_critical_region(t_calc, t_table, dof, tail=tail, direction="right")
