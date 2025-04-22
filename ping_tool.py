from pythonping import ping
from popular_domains import popular_domains
from datetime import datetime
from art import *

LOG_FILE = "ping_log.txt"
MAX_ALLOWED_RTT = 100


def log_result(message):
    """Запись результата в лог-файл"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def ping_server(host):
    timeout_ms = 90
    try:
        result = ping(host, count=4, timeout=timeout_ms / 1000)

        if result.rtt_avg_ms >= MAX_ALLOWED_RTT:
            raise Exception(f"Timeout - slow response ({result.rtt_avg_ms:.2f} ms ≥ {MAX_ALLOWED_RTT} ms)")

        success_msg = f"✅ {host}: {result.rtt_avg_ms:.2f} ms"
        print(success_msg)
        log_result(success_msg)
        return True

    except Exception as e:
        error_msg = f"🔴 {host}: {str(e)}"
        print(f"\n{error_msg}")
        log_result(error_msg)
        return False


def ping_from_file(filename):
    try:
        with open(filename) as f:
            domains = [d.strip() for d in f if d.strip()]

        log_result(f"Начата проверка файла: {filename} ({len(domains)} доменов)")
        print(f"\nПроверка {len(domains)} доменов из {filename}:")
        [ping_server(d) for d in domains]

    except Exception as e:
        error_msg = f"Ошибка при работе с файлом: {str(e)}"
        print(f"\n❌ {error_msg}")
        log_result(error_msg)



actions = {
    '1': lambda: ping_server(input("Введите домен: ")),
    '2': lambda: ping_from_file(input("Введите название файла txt с доменами: ")),
    '3': lambda: (
        log_result(f"Начата проверка списка доменов ({len(popular_domains)} шт.)"),
        [ping_server(d) for d in popular_domains]
    )
}

art = text2art("HASIK                 MUDAK")
print(f"{art}")

if __name__ == "__main__":
    try:
        while True:
            log_result("=" * 40 + " Запуск программы " + "=" * 40)
            try:
                mode = input("Режим (1-ручной, 2-файл, 3-список, 0-выход): ")
                if mode == '0':
                    log_result("=" * 40 + " Завершение работы " + "=" * 37 + "\n")
                    break
                actions.get(mode, lambda: print("❌ Неверный режим"))()
            except Exception as e:
                log_result(f"Критическая ошибка: {str(e)}")
            finally:
                log_result("=" * 40 + " Конец итерации " + "=" * 40 + "\n")
    except KeyboardInterrupt:
        log_result("=" * 40 + " Программа прервана пользователем " + "=" * 25 + "\n")