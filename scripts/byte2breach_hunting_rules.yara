rule APT_ByteToBreach_Sliver_C2_Implant {
    meta:
        author = "Antigravity Forensics"
        description = "Detects Sliver C2 linux/amd64 payloads connecting to known ByteToBreach infrastructure"
        threat_level = "CRITICAL"
        date = "2026-04-06"
        reference = "Sterling Bank SIFMIS Incident - ams-1118 Drop Node"

    strings:
        // C2 Connection Signatures
        $ip1 = "196.41.84.199" ascii wide
        $ip2 = "18.179.19.44" ascii wide
        $port1 = "50635" ascii wide
        $port2 = "57716" ascii wide
        
        // Target Environment Strings
        $env_target1 = "enf-fe-pilot" ascii wide
        $env_target2 = "4c1ce4744c9a" ascii wide
        $user1 = "nextjs" ascii wide
        $user2 = "tomcat" ascii wide

        // Sliver defaults built into the binary
        $sliver1 = "github.com/bishopfox/sliver" ascii wide
        $sliver2 = "sliver/client/transport" ascii wide

    condition:
        uint16(0) == 0x457f or uint16(0) == 0x5a4d // ELF or MZ header
        and (
            ($sliver1 or $sliver2) and
            (any of ($ip*) or any of ($env_target*))
        )
}

rule APT_ByteToBreach_AD_NodeDumper {
    meta:
        author = "Antigravity Forensics"
        description = "Detects the specific Node.js script used to map Sterling Bank's Active Directory and target the Managing Director/CEO."
        threat_level = "HIGH"

    strings:
        $var1 = "CHAIN LEVEL 3: Adebayodd" ascii wide
        $var2 = "CHAIN LEVEL 4: Ukachukwuao" ascii wide
        $target_role = "Managing Director/CEO" ascii wide
        $target_name = "Abubakar.Suleiman" ascii wide
        
        $json_field1 = "\"staffId\":\"" ascii wide
        $json_field2 = "\"supervisorName\":\"" ascii wide
        $json_field3 = "\"departmentName\":\"" ascii wide
        
        $error_rtgs = "DECRYPT RTGS LOGIN ERRORS" ascii wide
        $error_bsf = "DECRYPT BSF LOGIN ERRORS" ascii wide

    condition:
        5 of them
}

rule APT_ByteToBreach_Financial_JSON_Parser {
    meta:
        author = "Antigravity Forensics"
        description = "Detects shell scripts or JSON payloads parsing the Nigerian Inter-Bank routing array (BICs, Bank Codes) on Linux terminals."
        threat_level = "CRITICAL"

    strings:
        // Parsing Strings from ams-1118 root shell
        $bank1 = "FIRST SECURITIES DISCOUNT HOUSE" ascii wide
        $bank2 = "9 PAYMENT SERVICE BANK" ascii wide
        $bank3 = "ALPHA MORGAN BANK LIMITED" ascii wide
        $bank4 = "CORONATION MERCHANT BANK" ascii wide
        $bank5 = "GLOBUS BANK LIMITED" ascii wide

        // Code structures
        $json_structure1 = "{\"accountNumber\":\"" ascii wide
        $json_structure2 = "\",\"bankName\":\"" ascii wide
        $json_structure3 = "\",\"currency\":\"NGN\",\"bic\":\"" ascii wide
        $json_structure4 = "\",\"bankCode\":\"0" ascii wide

    condition:
        all of ($json_structure*) and 2 of ($bank*)
}
