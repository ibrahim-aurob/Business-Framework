<?php
// Nimmt die Anfrage entgegen, schickt sie mit Anhängen an AUROB
// und sendet dem Interessenten eine Eingangsbestätigung.

declare(strict_types=1);
require __DIR__ . '/inc/lib.php';

guard();
$c = cfg();

$d = [
    'menge'       => field('menge', 20),
    'bedarf'      => field('bedarf', 60),
    'werkstoff'   => field('werkstoff', 200),
    'oberflaeche' => field('oberflaeche', 200),
    'durchmesser' => field('durchmesser', 20),
    'laenge'      => field('laenge', 20),
    'name'        => oneline(field('name', 120)),
    'firma'       => oneline(field('firma', 160)),
    'email'       => oneline(field('email', 200)),
    'telefon'     => oneline(field('telefon', 60)),
    'termin'      => field('termin', 120),
    'land'        => field('land', 40),
    'nachricht'   => field('nachricht', 4000),
    'einwilligung'=> field('einwilligung', 5),
];

if ((int)$d['menge'] < 1)            { respond(false, '', 'Bitte geben Sie eine Stückzahl an.'); }
if ($d['name'] === '' || $d['firma'] === '') { respond(false, '', 'Bitte geben Sie Name und Firma an.'); }
if (!valid_email($d['email']))       { respond(false, '', 'Bitte prüfen Sie Ihre E-Mail-Adresse.'); }
if ($d['einwilligung'] !== 'ja')     { respond(false, '', 'Bitte stimmen Sie der Datenverarbeitung zu.'); }

// ---------- Dateien prüfen ----------
$anhaenge = [];
$summe = 0;
if (!empty($_FILES['dateien']) && is_array($_FILES['dateien']['name'])) {
    $n = count($_FILES['dateien']['name']);
    for ($i = 0; $i < $n; $i++) {
        $err = $_FILES['dateien']['error'][$i];
        if ($err === UPLOAD_ERR_NO_FILE) { continue; }
        if ($err !== UPLOAD_ERR_OK) { respond(false, '', 'Eine Datei konnte nicht hochgeladen werden. Bitte senden Sie große Dateien per E-Mail.'); }
        $orig = basename((string)$_FILES['dateien']['name'][$i]);
        $ext  = strtolower(pathinfo($orig, PATHINFO_EXTENSION));
        if (!in_array($ext, $c['endungen'], true)) { respond(false, '', 'Dateityp nicht erlaubt: ' . $orig); }
        $tmp = (string)$_FILES['dateien']['tmp_name'][$i];
        if (!is_uploaded_file($tmp)) { continue; }
        $summe += (int)$_FILES['dateien']['size'][$i];
        if (count($anhaenge) >= $c['max_dateien'] || $summe > $c['max_bytes']) {
            respond(false, '', 'Maximal ' . $c['max_dateien'] . ' Dateien und 20 MB. Größere Dateien bitte per E-Mail.');
        }
        $safe = preg_replace('/[^A-Za-z0-9._-]+/', '_', $orig) ?: ('datei.' . $ext);
        $anhaenge[] = ['name' => $safe, 'pfad' => $tmp, 'typ' => 'application/octet-stream'];
    }
}

// ---------- Mail an AUROB ----------
$zeilen = [
    'Stückzahl'   => $d['menge'] . ' (' . $d['bedarf'] . ')',
    'Werkstoff'   => $d['werkstoff'] ?: '–',
    'Oberfläche'  => $d['oberflaeche'] ?: '–',
    'Ø / Länge'   => ($d['durchmesser'] ?: '–') . ' mm / ' . ($d['laenge'] ?: '–') . ' mm',
    'Wunschtermin'=> $d['termin'] ?: '–',
    'Lieferland'  => $d['land'],
    'Dateien'     => $anhaenge ? implode(', ', array_column($anhaenge, 'name')) : 'keine',
    ''            => '',
    'Name'        => $d['name'],
    'Firma'       => $d['firma'],
    'E-Mail'      => $d['email'],
    'Telefon'     => $d['telefon'] ?: '–',
];
$text = "Neue Anfrage über serienteile-cnc-drehen.de\n\n";
foreach ($zeilen as $k => $v) { $text .= $k === '' ? "\n" : mb_str_pad($k . ':', 14) . $v . "\n"; }
$text .= "\nAnmerkungen:\n" . ($d['nachricht'] ?: '–') . "\n\n"
       . 'Eingang: ' . date('d.m.Y H:i') . " Uhr\nAntwort-Ziel: innerhalb von 48 Stunden\n";

$betreff = 'Anfrage: ' . $d['menge'] . ' Stk · ' . $d['firma'] . ($d['werkstoff'] ? ' · ' . $d['werkstoff'] : '');

if (!send_mail($c['empfaenger'], $betreff, $text, $d['email'], $anhaenge)) {
    respond(false, '', 'Die Anfrage konnte nicht versendet werden.');
}

// ---------- Eingangsbestätigung an den Interessenten ----------
$anrede = 'Guten Tag ' . $d['name'] . ',';
$bestaetigung = $anrede . "\n\n"
  . "danke für Ihre Anfrage. Sie ist bei uns angekommen.\n\n"
  . "So geht es weiter:\n"
  . "1. Wir prüfen Ihre Zeichnung und Angaben.\n"
  . "2. Bei Rückfragen melden wir uns kurz telefonisch oder per E-Mail.\n"
  . "3. Innerhalb von 48 Stunden erhalten Sie Ihr Angebot.\n\n"
  . "Ihre Angaben:\n"
  . '- Stückzahl: ' . $d['menge'] . ' (' . $d['bedarf'] . ")\n"
  . '- Werkstoff: ' . ($d['werkstoff'] ?: 'laut Zeichnung') . "\n"
  . '- Dateien: ' . ($anhaenge ? count($anhaenge) : 'keine') . "\n\n"
  . "Etwas vergessen? Antworten Sie einfach auf diese E-Mail.\n\n"
  . "Viele Grüße\nIhr AUROB-Team\n" . $c['basis_url'] . "\n";

send_mail($d['email'], 'Ihre Anfrage ist eingegangen – AUROB Serien-Drehteile', $bestaetigung, $c['empfaenger']);

webhook(['typ' => 'anfrage', 'zeit' => date('c'), 'daten' => $d, 'dateien' => array_column($anhaenge, 'name')]);

respond(true, 'danke.html');
