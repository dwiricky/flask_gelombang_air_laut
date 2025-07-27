from flask import Flask, render_template, request
import pandas as pd

# Inisialisasi Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    tinggi = 1.5
    periode = 10
    lebar = 30
    efisiensi = 85
    waktu = 24
    capex = 100000000
    opex = 5000000
    diskonto = 10
    harga_listrik = 1000
    lci = 50  
    coe = 100  

    # Memeriksa apakah ada data yang diinput oleh pengguna
    if request.method == 'POST':
        tinggi = float(request.form.get('tinggi-gelombang', 1.5)) 
        periode = float(request.form.get('periode-gelombang', 10))
        lebar = float(request.form.get('lebar-serap', 30))
        efisiensi = float(request.form.get('efisiensi-konversi', 85))
        waktu = float(request.form.get('waktu-operasional', 24))
        capex = float(request.form.get('capex', 100000000))
        opex = float(request.form.get('opex', 5000000))
        diskonto = float(request.form.get('diskonto', 10))
        harga_listrik = float(request.form.get('harga-listrik', 1000))
        lci = float(request.form.get('lci', 50))
        coe = float(request.form.get('coe', 100))

    # Perhitungan untuk demo
    daya_gelombang = tinggi * lebar * efisiensi / 100  # kW/m
    produksi_energi = daya_gelombang * waktu * 365  # kWh/tahun

    # Perhitungan finansial
    npv = capex - (produksi_energi * harga_listrik) / (1 + diskonto / 100)
    irr = (produksi_energi * harga_listrik - opex) / capex * 100
    pp = capex / (produksi_energi * harga_listrik - opex)
    dpp = capex / ((produksi_energi * harga_listrik - opex) / (1 + diskonto / 100))
    pi = (npv + capex) / capex
    lcoe = (capex + opex) / produksi_energi

    # Menentukan status Layak/Impas/Tidak Layak
    status_np = "Layak" if npv > 0 else "Impas" if npv == 0 else "Tidak Layak"
    status_irr = "Layak" if irr > diskonto else "Tidak Layak"
    status_pp = "Layak" if pp < 5 else "Tidak Layak"  
    status_dpp = "Layak" if dpp < 5 else "Tidak Layak"  
    status_pi = "Layak" if pi > 1 else "Tidak Layak"  
    status_lcoe = "Layak" if lcoe < 500 else "Tidak Layak"  
    
    # Mengirimkan data ke template
    data = {
        "npv": npv,
        "irr": irr,
        "pp": pp,
        "dpp": dpp,
        "pi": pi,
        "lcoe": lcoe,
        "status_np": status_np,
        "status_irr": status_irr,
        "status_pp": status_pp,
        "status_dpp": status_dpp,
        "status_pi": status_pi,
        "status_lcoe": status_lcoe,
        "years": [2021, 2022, 2023],
        "pendapatan_tahunan": [produksi_energi * harga_listrik] * 3,
        "biaya_tahunan": [opex] * 3,
        "daya_gelombang": daya_gelombang,
        "produksi_energi": produksi_energi
    }

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
