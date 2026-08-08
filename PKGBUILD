pkgname=declan
pkgver=1.1
pkgrel=1

pkgdesc="Tiny utility to manage Arch-based Linux declaratively"
arch=("any")
url="https://github.com/monikrab/declan"
license=("GPL-2.0")

depends=("python" "git" "man-db")
optdepends=(
    "yay: for 'relay' and 'rebuild'"
    "pv: for 'backup'"
    "github-cli: for 'rice'"
)

Replace release tarball with main branch during beta

source=(
    "https://github.com/monikrab/declan/archive/refs/tags/v${pkgver}.tar.gz"
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
