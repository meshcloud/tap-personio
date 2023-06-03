{ pkgs ? import <nixpkgs> { } }:
let
  unstable = import <nixpkgs-unstable> { }; 
  my-python = pkgs.python310; 
  python-with-my-packages =
    my-python.withPackages (p: with p; [ pip cookiecutter tox virtualenv ]);

in
pkgs.mkShell {
  NIX_SHELL = "tap-personio";
  buildInputs = [
    python-with-my-packages

    # these are used for build scripts/tools
    pkgs.yq
  ];
  shellHook = ''
    PYTHONPATH=${python-with-my-packages}/${python-with-my-packages.sitePackages}

    echo "Welcome to tap-personio"
  '';
}
