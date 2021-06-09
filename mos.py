import platform
from subprocess import check_output
import sys

def ping(host, ping_count):
    ping_str = f"-l 64 -n {ping_count}" if platform.system().lower() == "windows" else f"-c {ping_count}"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if platform.system().lower() == "windows" else True

    return check_output(args, shell=need_sh)


def calculate_jitter(output):
    reply_lines = [line for line in output.split("\n") if "time=" in line]
    latency_list = []

    for line in reply_lines:   # find latency per ping
        start = line.find("time=")
        end = line.find("ms")
        if platform.system().lower() == "windows":
            latency = int(line[start+5:end])
        else:
            latency = float(line[start+5:end-1])
        latency_list.append(latency)

    jitter = 0
    for i in range(len(latency_list)):   # calculate jitter based on latency
        if i == len(latency_list)-1:
            break
        elif latency_list[i] > latency_list[i+1]:
            jitter += latency_list[i] - latency_list[i+1]
        else:
            jitter += latency_list[i+1] - latency_list[i]

    return jitter / (len(latency_list)-1)


def fetch_average_latency(output):
    if platform.system().lower() == "windows":
        average_line = [line for line in output.split("\r\n") if "Average" in line]
        return int(str(average_line).split()[-1].strip("ms']"))

    else:
        average_line = [line for line in output.split("\n") if "avg" in line]
        return float(str(average_line).split("/")[-3])


def fetch_packet_loss(output):
    if platform.system().lower() == "windows":
        loss_line = [line for line in output.split("\r\n") if "loss" in line]
        return float(str(loss_line).split()[-2].strip("(").strip("%"))

    else:
        loss_line = [line for line in output.split("\n") if "loss" in line]
        if platform.system().lower() == "darwin":
            return float(str(loss_line).split()[-3].strip("%"))
        else:
            return float(str(loss_line).split()[-5].strip("%"))


def calculate_mos(jitter, packet_loss, latency, codec_delay):
    effective_latency = latency + jitter*2 + codec_delay
    if effective_latency < 160:
        r = 93.2 - (effective_latency / 40)
    else:
        r = 93.2 -((effective_latency - 120) / 10)

    r -= 2.5 * packet_loss
    if r < 0:
        mos = 1.0
    else:
        mos = 1 + 0.035*r + 0.000007*r*(r-60)*(100-r)

    return mos


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python mos.py <ip address> <ping count>")
        exit()
    host = sys.argv[1]
    ping_count = sys.argv[2]

output = (ping(host, ping_count)).decode("utf-8")
jitter = calculate_jitter(output)
packet_loss = fetch_packet_loss(output)
latency = fetch_average_latency(output)
codec_delay = 10.0
mos = calculate_mos(jitter, packet_loss, latency, codec_delay)




print("\n=====================================\n")
print(f"Mean Opinion Score (MOS): {mos:.4f}")
print("\n=====================================\n")
print(f"Data is based on {ping_count} pings (64 bytes) done towards IP address: {host}.")
print(f"** calculated with a codec delay of {codec_delay} **")