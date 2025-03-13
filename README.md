# next-research_s8

Documatation for Detection Apps

    ⚡Aplikasi ini dibangun menggunakan framework python yaitu flask.

    Mohon perhatian sebelum menjalankan aplikasi:
    ⚠️ Mohon melakukan instaling pip:
        ℹ️ pandas, numpy, flask, mysql_connector, os, glob, PIL, keras_facenet
    ⚠️ Mohon membangun database menggunakan nama unimed dan table dengan nama user.
    ⚠️ Dalam tabel user buatkan kolom:
        ℹ️ nim => Varchar(20) PRIMARY KEY
        ℹ️ nama => Varchar(50)
        ℹ️ unitKerja => Varchar (50)

    Adapun folder path didalam proyek ini adalah:
    📂src => berisikan seluruh program logika aplikasi hingga model melakukan pengenalan wajah.
    📂static => berisikan file yang digunakan untuk logika antarmuka aplikasi hingga foto wajah pengguna.
    📂templates => berisikan seluruh kerangka aplikasi.

    File-file penting yang harus di periksa saat aplikasi di jalankan.

    🗃️server.py
        ℹ️ Logika utama dalam menjalanakan aplikasi.
        ['Blueprint server'](./gambar_readme/image.png)
        ℹ️ Fungsi dari kode ini untuk menjalakan blueprint. Secara sederhananya digunakan untuk akses endpoint selain main atau indeks.html

    📂src
    Dalam folder ini terdapat beberapa folder lainnya, selain itu terdapat file __inti__.py yang berfungsi untuk melakukan pengimportan file-file dari folder lainya.

    📂model
        ℹ️Folder ini berisikan 5 file sebagai berikut:
            🗃️ data.pkl => berfungsi untuk menyimpan vektor wajah yang sudah melakukan registrasi.
            🗃️ facenet_keras.h5 => merupakan file yang berisikan model facenet yang digunakan untuk melakukan pengenalan wajah.
            🗃️ haarcascade....xml => merupakan file yang berisikan model untuk melakukan labeling wajah.
            🗃️ machine.py => merupakan file yang bertugas untuk melakukan pengekstraksi model dan pengenalan wajah yang melakukan registrasi.
            🗃️ save.py => berfungsi untuk melakukan penyimpanan data ke database mysql.

    📂 router
        ℹ️ Terdapat 2 file penting :
            🗃️ db.py => berfungsi untuk melakukan koneksi ke database. Keluaran dari file ini ada 2 yaitu conn sebagai koneksi dan cursor sebagai eksekusi query sql.

            ['Database connection setting](./gambar_readme/db.png)
            ⚠️ Mohon perhatikan bagian port. Untuk melakukan setting silahkan ikuti langkah berikut.
                ['Tampilan XAMPP'](./gambar_readme/xampp.png)
                ℹ️ Buka Xampp anda dan lihat bagian port di sebelah tombol start.
                ℹ️ Pada gambar port adalah 3307 maka seting pada db.py bagian function init_db() bagian conn silahkan ubah port sesuai xampp.

            🗃️ router.py => berisikan seluruh blueprint untuk akses endpoint setiap templates.

    ⚠️⚠️⚠️ MOHON DIPERHATIKAN SETIAP FUNCTION DI DALAM FILE ROUTER.PY REDAIRECT KE SAVE.PY DAN MACHINE.PY
