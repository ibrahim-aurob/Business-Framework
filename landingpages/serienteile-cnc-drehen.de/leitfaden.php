<?php
// Leadmagnet: schickt den Leitfaden per E-Mail und meldet den Lead an AUROB.

declare(strict_types=1);
require __DIR__ . '/inc/lib.php';

guard();
$c = cfg();

$email = oneline(field('email', 200));
if (!valid_email($email)) { respond(false, '', 'Bitte prüfen Sie Ihre E-Mail-Adresse.'); }

$link = $c['basis_url'] . $c['leitfaden'];

$text = "Guten Tag,\n\n"
  . "hier ist Ihr Leitfaden „Drehteile günstiger konstruieren – 12 Hebel für Serien ab 100 Stück“:\n\n"
  . $link . "\n\n"
  . "Tipp: Auf der letzten Seite steht eine Checkliste für eine vollständige Anfrage.\n"
  . "Damit bekommen Sie schneller ein genaues Angebot.\n\n"
  . "Sie haben schon eine Zeichnung? Dann schicken Sie sie uns.\n"
  . "Sie bekommen innerhalb von 48 Stunden einen Stückpreis – mit Hinweisen, wo Sie sparen können:\n"
  . $c['basis_url'] . "/#anfrage\n\n"
  . "Viele Grüße\nIhr AUROB-Team\n\n"
  . "Sie erhalten diese E-Mail, weil Sie den Leitfaden auf serienteile-cnc-drehen.de angefordert haben.\n"
  . "Wir schicken Ihnen keinen Newsletter.\n";

if (!send_mail($email, 'Ihr Leitfaden: Drehteile günstiger konstruieren', $text, $c['empfaenger'])) {
    respond(false, '', 'Der Leitfaden konnte nicht versendet werden.');
}

send_mail($c['empfaenger'], 'Leitfaden-Lead: ' . $email,
    "Neuer Leitfaden-Download über serienteile-cnc-drehen.de\n\nE-Mail: " . $email . "\nZeit: " . date('d.m.Y H:i') . " Uhr\n\n"
    . "Nachfassen: in 2–3 Tagen kurz anrufen oder eine persönliche E-Mail schicken (siehe FUNNEL.md).\n",
    $email);

webhook(['typ' => 'leitfaden', 'zeit' => date('c'), 'email' => $email]);

respond(true, 'danke-leitfaden.html');
