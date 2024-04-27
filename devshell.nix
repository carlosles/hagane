{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python312.withPackages(ps: []);
in
  pkgs.mkShell {
    name = "devshell";
    packages = [ pythonEnv ];
    shellHook = ''
      python -m venv .venv
      source .venv/bin/activate
    '';
  }
