package = "environments"
version = "dev-1"
source = {
   url = "git+https://github.com/pyrlkit/pyrlkit.git"
}
description = {
   homepage = "https://github.com/pyrlkit/pyrlkit",
   license = "*** please specify a license ***"
}
build = {
   type = "builtin",
   modules = {
      main = "main.lua"
   }
}
