# 📊 E-commerce Analytics Dashboard

Dashboard analitik e-commerce yang dibangun dengan Streamlit untuk visualisasi dan analisis data penjualan, pelanggan, dan performa pengiriman.

## Fitur

### Dashboard Multi-Tab
- **Performa Penjualan**: Analisis tren penjualan, profit, dan kategori produk
- **Analisis Pelanggan**: Segmentasi pelanggan dan analisis geografis
- **Performa Pengiriman**: Monitoring status pengiriman dan waktu delivery
- **Detail Data**: Statistik data dan viewer data mentah

### Interactive Filters
- Filter berdasarkan rentang tanggal
- Filter berdasarkan market (Africa, Europe, LATAM, Pacific Asia, USCA)
- Filter berdasarkan region pengiriman
- Filter berdasarkan segmen pelanggan (Consumer, Corporate, Home Office)
- Filter berdasarkan kategori produk

### Data Visualizations
- Tren penjualan dan profit harian
- Penjualan berdasarkan kategori produk dan region
- Pemetaan geografis penjualan
- Analisis segmentasi pelanggan
- Status pengiriman (tepat waktu, terlambat, lebih awal)
- Waktu pengiriman berdasarkan mode dan market
- Top 10 pelanggan dan region

### Key Metrics
- Total penjualan
- Total profit
- Jumlah pesanan
- Total item terjual
- Rata-rata waktu pengiriman

## Instalasi

### Prasyarat
- Python 3.7 atau lebih tinggi
- pip (Python package installer)

### Langkah Instalasi

1. **Clone atau download repository ini**
   ```bash
   git clone <repository-url>
   cd ecommerce-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Atau install secara manual:
   ```bash
   pip install streamlit pandas numpy plotly matplotlib seaborn
   ```

3. **Persiapkan data**
   - Pastikan file data CSV Anda bernama `ecommerce_data.csv`
   - Letakkan file tersebut di direktori yang sama dengan `dashboard.py`

4. **Jalankan dashboard**
   ```bash
   streamlit run dashboard.py
   ```

5. **Akses dashboard**
   - Buka browser dan akses `http://localhost:8501`

## 📁 Struktur File

```
ecommerce-dashboard/
├── dashboard.py           # File utama dashboard
├── ecommerce_data.csv    # File data (tidak termasuk dalam repo)
├── requirements.txt      # Dependencies
├── README.md            # Dokumentasi ini
```

## 📋 Format Data

Dashboard ini dirancang untuk dataset e-commerce dengan kolom-kolom berikut:

### Kolom Data Utama
| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `payment_type` | categorical | Jenis transaksi pembayaran |
| `profit_per_order` | numerical | Keuntungan per pesanan |
| `sales_per_customer` | numerical | Total penjualan per pelanggan |
| `category_id` | numerical | Kode kategori produk |
| `category_name` | text | Nama kategori produk |
| `customer_city` | categorical | Kota pelanggan |
| `customer_country` | categorical | Negara pelanggan |
| `customer_id` | numerical | ID pelanggan |
| `customer_segment` | categorical | Segmen pelanggan (Consumer, Corporate, Home Office) |
| `customer_state` | categorical | Provinsi/negara bagian pelanggan |
| `customer_zipcode` | text | Kode pos pelanggan |
| `order_date` | datetime | Tanggal pesanan |
| `order_id` | numerical | ID pesanan |
| `order_item_discount` | numerical | Nilai diskon item |
| `order_item_discount_rate` | numerical | Persentase diskon item |
| `order_item_quantity` | numerical | Jumlah produk per pesanan |
| `sales` | numerical | Nilai penjualan |
| `order_profit_per_order` | numerical | Profit per pesanan |
| `order_region` | categorical | Region pengiriman |
| `order_status` | categorical | Status pesanan |
| `shipping_date` | datetime | Tanggal pengiriman |
| `shipping_mode` | categorical | Mode pengiriman |
| `market` | categorical | Market tujuan |
| `label` | categorical | Status delivery (-1: early, 0: on time, 1: delayed) |

## 💡 Cara Penggunaan

### 1. Filter Data
- Gunakan sidebar untuk memfilter data berdasarkan periode waktu, market, region, segmen pelanggan, atau kategori produk
- Filter akan diterapkan secara real-time ke seluruh visualisasi

### 2. Navigasi Tab
- **Performa Penjualan**: Lihat tren penjualan, analisis kategori, dan profitabilitas
- **Analisis Pelanggan**: Analisis segmentasi pelanggan dan distribusi geografis
- **Performa Pengiriman**: Monitor status pengiriman dan waktu delivery
- **Detail Data**: Lihat statistik data dan browse data mentah

### 3. Interaksi dengan Grafik
- Hover untuk melihat detail data
- Zoom in/out pada grafik
- Download grafik sebagai PNG
- Toggle legend untuk hide/show data series

## 🎨 Kustomisasi

### Mengubah Tema
Untuk mengubah tema dashboard, edit bagian CSS dalam file `dashboard.py`:

```python
st.markdown("""
    <style>
    .main {
        background-color: #your-color;  # Ubah warna background
    }
    </style>
""", unsafe_allow_html=True)
```


## Dependencies

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- [Streamlit](https://streamlit.io/) - Framework web app
- [Plotly](https://plotly.com/) - Library visualisasi interaktif
- [Pandas](https://pandas.pydata.org/) - Data manipulation library
