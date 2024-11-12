import os
import json

data = {
                    "type": "WAKIL CALON",
                    "data": {
                        "image_url": "https://b-silonkada-prod.oss-ap-southeast-5.aliyuncs.com/berkas-silonkada/calon/3874/pas_foto/thumbnail_1729516276_16e450f8-c884-4c1e-aa2e-c3cf8b9e1411.jpeg?Expires=1730701322&OSSAccessKeyId=LTAI5t5nd46MND7D7BqdtifK&Signature=MOK5vdqudCuJ3Y3sFUkiMUsl78c%3D",
                        "name": "AGUSTINUS ANGGAIBAK, S.M.",
                        "details": {
                            "Jenis Kelamin": "Laki-laki",
                            "Tempat, Tanggal Lahir": "AGIMUGA, 17 Agustus 1980",
                            "Agama": "Kristen Katolik",
                            "Alamat": "MIMIKA, PAPUA TENGAH",
                            "Pendidikan Terakhir": "S1",
                            "Pekerjaan": "",
                            "Status Hukum": ""
                        },
                        "Pekerjaan": [
                            "WIRASWASTA"
                        ],
                        "Status Hukum": [
                            "Tidak memiliki status hukum"
                        ],
                        "Riwayat Pendidikan": [
                            {
                                "No": "1",
                                "Jenjang pendidikan": "S1",
                                "Institusi pendidikan": "STIE YAPAN SURABAYA",
                                "Gelar": "S.M",
                                "Tahun masuk": "2016",
                                "Tahun keluar": "2020"
                            },
                            {
                                "No": "2",
                                "Jenjang pendidikan": "SMA",
                                "Institusi pendidikan": "SMU YPPK TARUNA BHAKTI JAYAPURA",
                                "Gelar": "Data tidak ada",
                                "Tahun masuk": "1994",
                                "Tahun keluar": "1997"
                            },
                            {
                                "No": "3",
                                "Jenjang pendidikan": "SMP",
                                "Institusi pendidikan": "SMP YPPK KRISTEN KOTARAJA",
                                "Gelar": "Data tidak ada",
                                "Tahun masuk": "1991",
                                "Tahun keluar": "1994"
                            },
                            {
                                "No": "4",
                                "Jenjang pendidikan": "SD",
                                "Institusi pendidikan": "SD INPRES HARAPAN SENTANI JAYAPURA",
                                "Gelar": "Data tidak ada",
                                "Tahun masuk": "1985",
                                "Tahun keluar": "1991"
                            }
                        ],
                        "Riwayat Kursus/Diklat": [],
                        "Riwayat Organisasi": [
                            {
                                "No": "1",
                                "Nama organisasi": "Koperasi Peran Serta Masyarakat Mimika",
                                "Jabatan": "Ketua",
                                "Tahun masuk": "2002",
                                "Tahun keluar": "2006"
                            },
                            {
                                "No": "2",
                                "Nama organisasi": "Partai Golkar Distrik Agimuga",
                                "Jabatan": "Komdis",
                                "Tahun masuk": "2002",
                                "Tahun keluar": "2006"
                            },
                            {
                                "No": "3",
                                "Nama organisasi": "DPC Partai Hanura Kabupaten Mimika",
                                "Jabatan": "Ketua",
                                "Tahun masuk": "2008",
                                "Tahun keluar": "2013"
                            },
                            {
                                "No": "4",
                                "Nama organisasi": "Wakil Ketua VI DPD Golkar tiingkat II Kabupaten Mimika",
                                "Jabatan": "Wakil Ketua",
                                "Tahun masuk": "2023",
                                "Tahun keluar": "2027"
                            }
                        ],
                        "Riwayat Tanda Penghargaan": [],
                        "Riwayat Publikasi": [
                            {
                                "No": "1",
                                "Judul": "Agustinus Anggaibak jadi Ketua MRP Papua Tengah",
                                "Penerbit": "Timika Express",
                                "Tahun terbit": "2024"
                            },
                            {
                                "No": "2",
                                "Judul": "Ketua MRP Uji UU Otsus Papua Soal Nominasi Kepala Daerah",
                                "Penerbit": "Mkri.id",
                                "Tahun terbit": "2024"
                            },
                            {
                                "No": "3",
                                "Judul": "MRP Minta Pilkada Papua diisi Orang Asli Papua",
                                "Penerbit": "Metrotvnews.com",
                                "Tahun terbit": "2024"
                            },
                            {
                                "No": "4",
                                "Judul": "Bertemu Presiden Jokowi, MRP minta jabatan Bupati dan Wali Kota diisi Orang Asli Papua",
                                "Penerbit": "Kompas.tv",
                                "Tahun terbit": "2024"
                            },
                            {
                                "No": "5",
                                "Judul": "Ketua MRP PPT tegaskan ke Lemasa dan Lemasko Jangan Bentuk Banyak Kubu",
                                "Penerbit": "Lintastimor.com",
                                "Tahun terbit": "2024"
                            },
                            {
                                "No": "6",
                                "Judul": "Banyak hal MRP sampaikan ke Presiden Jokowi, apa saja?",
                                "Penerbit": "Suarapapua.com",
                                "Tahun terbit": "2024"
                            }
                        ]
                    },
                    "calon_id": "3874"
                }

def format_experience(item, type='education'):
    if type == 'education':
        pendidikan = item['Riwayat Pendidikan']
        kursus = item['Riwayat Kursus/Diklat']
        detail = pendidikan + kursus
    elif type == 'work':
        detail = item['Pekerjaan']
    elif type == 'organisation':
        detail = item['Riwayat Organisasi']

    experiences = []

    for experience_item in detail:
        x = {}

        # ORGANISASI
        # {
        #     "No": "1",
        #     "Nama organisasi": "Ketua Pengurus Daerah Padangpanjang Ikatan Da’i Indonesia (IKADI)",
        #     "Jabatan": "ketua",
        #     "Tahun masuk": "2007",
        #     "Tahun keluar": "2011"
        # },

        # PENDIDIKAN
        # {
        #     "No": "1",
        #     "Jenjang pendidikan": "SMA",
        #     "Institusi pendidikan": "SMA SUMBAWA",
        #     "Gelar": "Data tidak ada",
        #     "Tahun masuk": "1971",
        #     "Tahun keluar": "1974"
        # },

        # PEKERJAAN
        # "Pekerjaan": [
        #     "Konsultan/Pelatih pada Edu Consultant Indonesia\t [2019 s.d sekarang]"
        # ],

        currentYear = 2024

        if type == 'organisation':
            # EXAMPLE ORGANISATION:
            # {
            #     "current": true,
            #     "department": "Ikatan Alumnus SMP St.Yosef Surabaya",
            #     "description": "Pimpinan Ikatan Alumnus SMP St.Yosef Surabaya lintas angkatan",
            #     "endMonth": null,
            #     "endYear": null,
            #     "location": "jl.Joyoboyo no.19",
            #     "name": "Ketua Alumnus",
            #     "startMonth": "Oktober",
            #     "startYear": "2021"
            # },

            int_end_year = int(experience_item['Tahun keluar'])

            x['current'] = True if int_end_year > currentYear else False
            x['department'] = experience_item['Nama organisasi']
            x['description'] = None
            x['endMonth'] = None
            x['endYear'] = experience_item['Tahun keluar']
            x['location'] = None
            x['name'] = experience_item['Jabatan']
            x['startMonth'] = None
            x['startYear'] = experience_item['Tahun masuk']

        elif type == 'education':
            # EXAMPLE EDUCATION:
            # {
            #     "category": "Strata 2 - Magister",
            #     "department": "Managemen Keuangan dan Pemasaran Pelayanan Kesehatan",
            #     "endMonth": "Maret",
            #     "endYear": "2003",
            #     "location": "Jl Airlangga Kec Gubeng Surabaya",
            #     "name": "Pascasarjana Universitas Airlangga Surabaya",
            #     "startMonth": "Maret",
            #     "startYear": "2001"
            # },

            try:
                category = experience_item['Jenjang pendidikan']
            except:
                category = None

            try:
                department = experience_item['Institusi pendidikan']
            except:
                department = experience_item['Lembaga penyelenggara']

            try:
                name = experience_item['Gelar']
            except:
                name = experience_item['Nama kursus dan diklat']

            x['category'] = category
            x['department'] = department
            x['endMonth'] = None
            x['endYear'] = experience_item['Tahun keluar']
            x['name'] = name
            x['startMonth'] = None
            x['startYear'] = experience_item['Tahun masuk']

        elif type == 'work':
            # EXAMPLE PEKERJAAN:
            # {
            #     "category": "Lainnya",
            #     "current": true,
            #     "department": "Yayasan Pondok Kasih",
            #     "description": "Direktur MarCom memimpin\nDep Media and Promotion\nDep Public Relation (7 Sphere's)",
            #     "endMonth": null,
            #     "endYear": null,
            #     "jobType": "Full Time",
            #     "location": "Kendangsari 2 no.82 Surabaya",
            #     "name": "Direktur Marketing And Communication ",
            #     "startMonth": "Januari",
            #     "startYear": "2021"
            # },

            x['category'] = 'Lainnya'
            x['current'] = False
            x['department'] = None
            x['description'] = None
            x['endMonth'] = None
            x['endYear'] = None
            x['jobType'] = None
            x['location'] = None
            x['name'] = experience_item
            x['startMonth'] = None
            x['startYear'] = None


        experiences.append(x)

    return experiences


result = {}
# format experience
result['pendidikan'] = format_experience(data['data'], 'education')
result['pekerjaan'] = format_experience(data['data'], 'work')
result['organisasi'] = format_experience(data['data'], 'organisation')


# save to result.json
with open('result.json', 'w') as f:
    json.dump(result, f, indent=4)