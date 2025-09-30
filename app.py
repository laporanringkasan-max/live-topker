import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import io, matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- TITLE PAGE --- #
st.set_page_config(page_title="LIVE TOPKER", layout="wide")
st.title("📈 LIVE TOPKER")

# --- UPLOAD FILE --- #
file = st.file_uploader("Unggah File (.xlsx)", type=["xlsx"], key="excel_uploader")

# --- PILIH TANGGAL ---- #
d1, d2 = st.columns(2)

with d1:
    start_date = st.date_input("Tanggal Mulai")
with d2:
    end_date = st.date_input("Tanggal Akhir")
print(start_date)
print(end_date)

# --- PILIH METRIK ---- #
c1, c2, c3, c4, c5, c6 = st.columns(6)
metrik_dipilih = []
with c1:
    metrik1 = st.checkbox("GMV")
with c2:
    metrik2 = st.checkbox("Impresi Live")
with c3:
    metrik3 = st.checkbox("Kunjungan Live")
with c4:
    metrik4 = st.checkbox("Impresi Produk")
with c5:
    metrik5 = st.checkbox("Klik Produk")
with c6:
    metrik6 = st.checkbox("Jumlah Pembayaran")

if metrik1:
    metrik_dipilih.append("GMV")
if metrik2:
    metrik_dipilih.append("IMPRESI LIVE")
if metrik3:
    metrik_dipilih.append("KUNJUNGAN LIVE")
if metrik4:
    metrik_dipilih.append("IMPRESI PRODUK")
if metrik5:
    metrik_dipilih.append("KLIK PRODUK")
if metrik6:
    metrik_dipilih.append("JUMLAH PEMBAYARAN")

# --- DATA --- #
if not file:
    st.info("Unggah file Excel untuk mulai.")
    st.stop()

try:
    df = pd.read_excel(file)
except Exception as e:
    st.error(f"Gagal membaca Excel: {e}")
    st.stop()

# Format Tanggal
df["TANGGAL"] = pd.to_datetime(df["TANGGAL"], format="%d/%m/%Y")

# Standarisasi GMV, IMPRESI LIVE,
scaler = MinMaxScaler()
df["GMV"] = scaler.fit_transform(df[["GMV"]])
df["IMPRESI LIVE"] = scaler.fit_transform(df[["IMPRESI LIVE"]])
df["KUNJUNGAN LIVE"] = scaler.fit_transform(df[["KUNJUNGAN LIVE"]])
df["IMPRESI PRODUK"] = scaler.fit_transform(df[["IMPRESI PRODUK"]])
df["KLIK PRODUK"] = scaler.fit_transform(df[["KLIK PRODUK"]])
df["JUMLAH PEMBAYARAN"] = scaler.fit_transform(df[["JUMLAH PEMBAYARAN"]])

# Filter df berdasarkan start date dan end date
start_date = pd.to_datetime(start_date, format="%d/%m/%Y")
end_date = pd.to_datetime(end_date, format="%d/%m/%Y")
df = df.query("TANGGAL >= @start_date and TANGGAL <= @end_date").reset_index(drop=True)

if df.empty or not metrik_dipilih:
    st.warning("Tidak ada data pada rentang tanggal/metrik yang dipilih.")
else:
    st.line_chart(df, x="TANGGAL", y=metrik_dipilih)

# --- Download Grafik --- #
fig, ax = plt.subplots(figsize=(8, 4.5))
for c in metrik_dipilih:
    ax.plot(df["TANGGAL"], df[c], label=c)
ax.set_xlabel("Tanggal"); ax.set_ylabel("Nilai"); ax.legend(); ax.grid(True)
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))  
fig.autofmt_xdate() 

buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight", dpi=200); buf.seek(0)
st.download_button("⬇️ Download Grafik", data=buf, file_name="grafik_live_topker.png", mime="image/png")