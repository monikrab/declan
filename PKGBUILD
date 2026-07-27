pkgname=declan
pkgver=1.1-beta
pkgrel=2

pkgdesc="Tiny utility to manage Arch Linux declaratively"
arch=("any")
url="https://github.com/monikrab/declan"
license=("GPL-2.0")

depends=("python" "git")
optdepends=(
    "yay: for 'relay' and 'rebuild'"
    "pv: for 'backup'"
    "github-cli: for 'rice'"
)

# Replace release tarball with main branch during beta
# 
# source=(
#     "https://github.com/monikrab/declan/archive/refs/tags/v${pkgver}.tar.gz"
# )
# sha256sums=("0432fc2eee8092f8757ad2025d5c7961a600722233c62bcc4c2cc4fe792bda6c")

source=(
    "git+https://github.com/monikrab/declan.git#branch=main"
)
sha256sums=('SKIP')

package() {
    install -Dm755 \
        "$srcdir/$pkgname-$pkgver/src/declan.py" \
        "$pkgdir/usr/bin/declan"

    install -Dm644 \
        "$srcdir/$pkgname-$pkgver/man/declan.1" \
        "$pkgdir/usr/share/man/man1/declan.1"
}
