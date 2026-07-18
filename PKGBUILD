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
sha256sums=('0432fc2eee8092f8757ad2025d5c7961a600722233c62bcc4c2cc4fe792bda6c')

package() {
    install -Dm755 \
        "$srcdir/$pkgname-$pkgver/src/declan.py" \
        "$pkgdir/usr/bin/declan"

    install -Dm644 \
        "$srcdir/$pkgname-$pkgver/man/declan.1" \
        "$pkgdir/usr/share/man/man1/declan.1"
}
