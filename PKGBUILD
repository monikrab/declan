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
sha256sums=('d160374d063a46a8bdeac939d9dd553c66ebb577f05125a0b22c7e41517682cf')

package() {
    install -Dm755 \
        "$srcdir/$pkgname-$pkgver/src/declan.py" \
        "$pkgdir/usr/bin/declan"

    install -Dm644 \
        "$srcdir/$pkgname-$pkgver/man/declan.1" \
        "$pkgdir/usr/share/man/man1/declan.1"
}
