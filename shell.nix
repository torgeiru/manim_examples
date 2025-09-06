{
  pkgs ? import <nixpkgs> {}
}
:
pkgs.mkShell {
  name = "";
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.manim
    ]))
  ];
}
