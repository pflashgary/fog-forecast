VAR=":TMP:2 m above ground:"
jq -r --arg var "$VAR" '
      .[]
    | .url as $url
    | .dirs[] | . as $yyyymm
    | range(1;32) | . | npad(2) as $dd
    | range(0;85) | . | npad(3) as $prog
    | $var | gsub(" "; "_") as $no_space_var
    | "\($url)\($yyyymm)/\($yyyymm)\($dd)/nam_218_\($yyyymm)\($dd)_0000_\($prog).grb2.inv" as $inv
    | "\($url)\($yyyymm)/\($yyyymm)\($dd)/nam_218_\($yyyymm)\($dd)_0000_\($prog).grb2" as $src_grib
    | "nam_218_\($yyyymm)\($dd)_0000_\($prog)_\($no_space_var).grb2" as $dst_grib
    | "echo ./get_inv.pl \($inv|@sh) | grep \($var|@sh) | ./get_grib.pl \($src_grib|@sh) \($dst_grib|@sh)"
' inv.json