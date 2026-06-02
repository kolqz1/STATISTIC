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

# 1. (Judul Hypotesis) <--

# Step 1: State null and alternate hypotesis
# H0: μ <= 200  <--
# H1: μ > 200   <--

# Step 2: Select the level of significance
sample = df['Average Combat Score']     # <-- df['column_name']
alpha = 0.05    # Level of significance
tail = 1     # one-tailed or two-tailed  <-- jika H0 '>=' atau '<=' isi 1, jika '=' isi 2


n = len(sample)
dof = n - 1 
Xbar = sample.mean()    # df[Column_name].mean()
Miu = 200     # claimnya  <--
s = sample.std(ddof=1)    # df[Column_name].std(ddof=1)

# # Step 3: Determine the test statistic  <--


# # Step 5: Make the decision regarding H0
t_calc = (Xbar - Miu) / (s / np.sqrt(n))
t_table = get_t_table(alpha, tail, dof)

print("t_calc = ", round(t_calc, 2))
print("t_table = ", round(t_table, 2))

# # Step 6: Interpret the result
if t_calc > t_table:  # <-- tandanya disesuaikan dengan syarat:
# jika H0 '>=' maka ganti dengan '<' atau
# jika H0 '<=' maka ganti dengan '>' atau
# jika H0 '=' maka ganti dengan 'abs(t_calc) >'
    print("H0 is rejected, the mean ACS of VCT player is higher than 200") # <-- tambahkan kesimpulan
else:
    print("H0 is fail to reject, the mean ACS of VCT player is not higher than 200") # <-- tambahkan kesimpulan


# plot_critical_region(t_calc, t_table, dof, tail=tail, direction="right")   <-- isi bagian direction dengan:
# (jika H0: '>=' maka 'right') atau 
# (jika H0: '<=' maka 'left') atau 
# (jika H0: '=' maka tidak usah di isi)

plot_critical_region(t_calc, t_table, dof, tail=tail, direction="right")
# jika sudah selesai, kirim filenya dengan format 'nomor hipotesa_(H0 berapa)' ke:
# https://drive.google.com/drive/folders/1DvBSf0U_tMFXIm6-jsvoYLS8aga8xVEu?usp=sharing
