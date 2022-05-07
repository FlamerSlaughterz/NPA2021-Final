from netmiko import ConnectHandler


def config_from_device(device_params, intf):
    with ConnectHandler(**device_params) as ssh:
        data = ssh.send_command("sh ip int br")
        result = data.strip().split("\n")
        has_loop_back = False
        for line in result[1:]:
            words = line.split()
            if words[0] == intf:
                has_loop_back = True
        if not has_loop_back:
            ssh.send_command_timing("configure terminal")
            ssh.send_command_timing("int "+intf)
            ssh.send_command_timing("ip add 192.168.1.1 255.255.255.0")
            ssh.send_command_timing("no shut")
            ssh.send_command_timing("end")

        else:
            ssh.send_command_timing("configure terminal")
            ssh.send_command_timing("no int lo62070202")
            ssh.send_command_timing("end")
        check_ans = ssh.send_command_timing("sh ip int br")


    return check_ans
        
if __name__ == '__main__':
    device_ip = "10.0.15.14"
    username = "admin"
    password = "cisco"

    device_params = {"device_type": "cisco_ios",
                    "ip": device_ip,
                    "username": username,
                    "password": password
                    }

    print(config_from_device(device_params, "Loopback62070202"))