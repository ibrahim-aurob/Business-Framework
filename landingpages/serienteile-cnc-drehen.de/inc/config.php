<?php
// Konfiguration für die Formulare. Diese Datei ist per .htaccess gesperrt.

return [
    // Hierhin gehen neue Anfragen und Leitfaden-Leads.
    'empfaenger'   => 'info@aurob.de',

    // Absender MUSS eine Adresse der eigenen Domain sein (SPF/DKIM bei all-inkl).
    // Im KAS anlegen: anfrage@serienteile-cnc-drehen.de
    'absender'     => 'anfrage@serienteile-cnc-drehen.de',
    'absender_name'=> 'AUROB Serien-Drehteile',

    // Basis-URL der Seite (für Links in E-Mails)
    'basis_url'    => 'https://serienteile-cnc-drehen.de',

    // Leitfaden-PDF (relativ zur Basis-URL)
    'leitfaden'    => '/leitfaden/AUROB-Leitfaden-Drehteile-guenstiger-konstruieren.pdf',

    // Uploads
    'max_dateien'  => 5,
    'max_bytes'    => 20 * 1024 * 1024,
    'endungen'     => ['pdf','step','stp','dxf','dwg','igs','iges','jpg','jpeg','png','zip'],

    // Schutz gegen Missbrauch
    'min_sekunden' => 3,     // schneller ausgefüllt = Bot
    'max_pro_std'  => 6,     // Anfragen pro IP und Stunde

    // Optional: Webhook (z. B. n8n), bekommt jede Anfrage als JSON. Leer = aus.
    'webhook_url'  => '',
];
