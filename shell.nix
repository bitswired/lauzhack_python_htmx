{ pkgs ? import <nixpkgs> {} }:


pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.python310
    pkgs.poetry
  ];
}
