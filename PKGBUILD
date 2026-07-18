pkgname=declan
pkgver=1.0
pkgrel=1
pkgdesc="Tiny utility to manage Arch Linux declaratively"
arch=('any')
url="https://github.com/monikrab/declan"
license=('GPL-2.0')
depends=('python' 'git')
optdepends=(
    'yay: for declan relay and declan rebuild'
    'pv: for declan backup'
    'github-cli: for declan rice'
)
source=(
    "https://github.com/monikrab/declan/archive/refs/tags/v${pkgver}.tar.gz"
)
sha256sums=('d1e708bc59ee4b541c68ab09fcb83d2dcce2045645f6ecaa8a09f53593100c35')

package() {
    install -Dm755 \
        "$srcdir/$pkgname-$pkgver/src/declan.py" \
        "$pkgdir/usr/bin/declan"

    install -Dm644 \
        "$srcdir/$pkgname-$pkgver/man/declan.1" \
        "$pkgdir/usr/share/man/man1/declan.1"
}
