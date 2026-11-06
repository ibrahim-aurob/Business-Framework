<?php
// Gemeinsame Funktionen für anfrage.php und leitfaden.php

declare(strict_types=1);

function cfg(): array {
    static $c = null;
    if ($c === null) { $c = require __DIR__ . '/config.php'; }
    return $c;
}

function wants_json(): bool {
    return isset($_SERVER['HTTP_ACCEPT']) && str_contains($_SERVER['HTTP_ACCEPT'], 'application/json');
}

function respond(bool $ok, string $redirect = '', string $error = ''): never {
    if (wants_json()) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'redirect' => $redirect, 'error' => $error], JSON_UNESCAPED_UNICODE);
        exit;
    }
    if ($ok) {
        header('Location: ' . $redirect, true, 303);
        exit;
    }
    http_response_code(400);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       . '<link rel="stylesheet" href="assets/css/style.css"><main class="page"><div class="wrap narrow">'
       . '<h1>Das hat nicht geklappt.</h1><p>' . h($error) . '</p>'
       . '<p><a class="btn" href="javascript:history.back()">← Zurück zum Formular</a></p>'
       . '<p>Oder schreiben Sie direkt an <a href="mailto:' . h(cfg()['empfaenger']) . '">' . h(cfg()['empfaenger']) . '</a>.</p>'
       . '</div></main>';
    exit;
}

function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

function field(string $k, int $max = 500): string {
    $v = $_POST[$k] ?? '';
    if (is_array($v)) { $v = implode(', ', array_map('strval', $v)); }
    $v = trim(str_replace(["\r", "\0"], '', (string)$v));
    return mb_substr($v, 0, $max);
}

/** Kopfzeilen-sicher: keine Zeilenumbrüche */
function oneline(string $s): string { return trim(preg_replace('/[\r\n\t]+/', ' ', $s) ?? ''); }

function guard(): void {
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { respond(false, '', 'Ungültiger Aufruf.'); }
    // Honeypot: Bots füllen das versteckte Feld
    if (field('website') !== '') { respond(true, 'danke.html'); }
    // Zu schnell ausgefüllt
    $ts = (int)field('ts', 20);
    if ($ts > 0 && (time() * 1000 - $ts) < cfg()['min_sekunden'] * 1000) { respond(true, 'danke.html'); }
    // Rate-Limit pro IP
    $dir = sys_get_temp_dir() . '/aurob-rl';
    if (!is_dir($dir)) { @mkdir($dir, 0700, true); }
    $key = $dir . '/' . hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . date('YmdH'));
    $n = is_file($key) ? (int)file_get_contents($key) : 0;
    if ($n >= cfg()['max_pro_std']) { respond(false, '', 'Zu viele Anfragen. Bitte versuchen Sie es später erneut.'); }
    @file_put_contents($key, (string)($n + 1));
}

function valid_email(string $e): bool {
    return (bool)filter_var($e, FILTER_VALIDATE_EMAIL) && !preg_match('/[\r\n]/', $e);
}

/**
 * Sendet eine E-Mail (Text + optional HTML) mit Anhängen über mail().
 * @param array $anhaenge Liste von ['name'=>..., 'pfad'=>..., 'typ'=>...]
 */
function send_mail(string $an, string $betreff, string $text, string $replyTo = '', array $anhaenge = [], string $html = ''): bool {
    $c = cfg();
    $eol = "\r\n";
    $from = '=?UTF-8?B?' . base64_encode($c['absender_name']) . '?= <' . $c['absender'] . '>';
    $headers  = 'From: ' . $from . $eol;
    if ($replyTo !== '' && valid_email($replyTo)) { $headers .= 'Reply-To: ' . $replyTo . $eol; }
    $headers .= 'MIME-Version: 1.0' . $eol;
    $headers .= 'X-Mailer: AUROB-Landingpage' . $eol;

    $b1 = 'b1_' . bin2hex(random_bytes(12));
    $b2 = 'b2_' . bin2hex(random_bytes(12));

    $alt  = '--' . $b2 . $eol . 'Content-Type: text/plain; charset=UTF-8' . $eol . 'Content-Transfer-Encoding: base64' . $eol . $eol
          . chunk_split(base64_encode($text)) . $eol;
    if ($html !== '') {
        $alt .= '--' . $b2 . $eol . 'Content-Type: text/html; charset=UTF-8' . $eol . 'Content-Transfer-Encoding: base64' . $eol . $eol
              . chunk_split(base64_encode($html)) . $eol;
    }
    $alt .= '--' . $b2 . '--' . $eol;

    if (!$anhaenge) {
        $headers .= 'Content-Type: multipart/alternative; boundary="' . $b2 . '"';
        $body = $alt;
    } else {
        $headers .= 'Content-Type: multipart/mixed; boundary="' . $b1 . '"';
        $body = '--' . $b1 . $eol . 'Content-Type: multipart/alternative; boundary="' . $b2 . '"' . $eol . $eol . $alt;
        foreach ($anhaenge as $a) {
            $name = preg_replace('/[^A-Za-z0-9._-]+/', '_', $a['name']);
            $body .= '--' . $b1 . $eol
                   . 'Content-Type: ' . $a['typ'] . '; name="' . $name . '"' . $eol
                   . 'Content-Transfer-Encoding: base64' . $eol
                   . 'Content-Disposition: attachment; filename="' . $name . '"' . $eol . $eol
                   . chunk_split(base64_encode((string)file_get_contents($a['pfad']))) . $eol;
        }
        $body .= '--' . $b1 . '--';
    }
    $subject = '=?UTF-8?B?' . base64_encode(oneline($betreff)) . '?=';
    return mail($an, $subject, $body, $headers, '-f' . $c['absender']);
}

function webhook(array $data): void {
    $url = cfg()['webhook_url'];
    if ($url === '') { return; }
    $ctx = stream_context_create(['http' => [
        'method' => 'POST', 'timeout' => 4,
        'header' => "Content-Type: application/json\r\n",
        'content' => json_encode($data, JSON_UNESCAPED_UNICODE),
    ]]);
    @file_get_contents($url, false, $ctx);
}
