#!/bin/bash
# test-18.171.217.18.sh - SCRIPT DI TEST COMPLETO

set -e

echo "🧪 Testing connectivity to 18.171.217.18"
echo "========================================="

# Funzione per test HTTP
test_endpoint() {
    local url=$1
    local description=$2
    echo -n "Testing $description ($url): "
    
    if curl -f -s -m 10 "$url" >/dev/null 2>&1; then
        echo "✅ OK"
        return 0
    else
        echo "❌ FAILED"
        return 1
    fi
}

# Test connettività di base
echo "🔌 Basic connectivity tests..."
ping -c 3 18.171.217.18 >/dev/null 2>&1 && echo "✅ Ping OK" || echo "❌ Ping FAILED"

# Test porte specifiche (se nmap è disponibile)
if command -v nmap >/dev/null 2>&1; then
    echo ""
    echo "🔍 Port scanning..."
    nmap -p 80,8000,443 18.171.217.18 2>/dev/null || echo "⚠️  nmap not available"
fi

echo ""
echo "🌐 HTTP endpoint tests..."

# Test endpoint principali
test_endpoint "http://18.171.217.18:8000/health" "Health Check (port 8000)"
test_endpoint "http://18.171.217.18/" "Homepage (port 80)"
test_endpoint "http://18.171.217.18:8000/docs" "API Documentation"
test_endpoint "http://18.171.217.18:8000/openapi.json" "OpenAPI Schema"

# Test con output dettagliato
echo ""
echo "🔍 Detailed health check..."
echo "----------------------------"
curl -v -m 15 http://18.171.217.18:8000/health 2>&1 || echo "❌ Detailed test failed"

# Test headers
echo ""
echo "📋 Response headers check..."
echo "----------------------------"
curl -I -m 10 http://18.171.217.18:8000/health 2>/dev/null || echo "❌ Headers check failed"

# Test JSON response
echo ""
echo "📊 JSON response test..."
echo "------------------------"
response=$(curl -s -m 10 http://18.171.217.18:8000/health 2>/dev/null)
if [ $? -eq 0 ] && echo "$response" | grep -q "status"; then
    echo "✅ Valid JSON response received"
    echo "$response" | head -5
else
    echo "❌ Invalid or no JSON response"
fi

# Test internal vs external
echo ""
echo "🏠 Internal vs External test..."
echo "-------------------------------"
if command -v docker >/dev/null 2>&1; then
    echo -n "Internal (localhost:8000): "
    curl -f -s -m 5 http://localhost:8000/health >/dev/null 2>&1 && echo "✅ OK" || echo "❌ FAILED"
fi

echo -n "External (18.171.217.18:8000): "
curl -f -s -m 10 http://18.171.217.18:8000/health >/dev/null 2>&1 && echo "✅ OK" || echo "❌ FAILED"

# Test traceroute (se disponibile)
if command -v traceroute >/dev/null 2>&1; then
    echo ""
    echo "🗺️  Network path to server..."
    echo "----------------------------"
    traceroute -m 10 18.171.217.18 2>/dev/null | head -5 || echo "⚠️  traceroute not available"
fi

# Diagnosi problemi comuni
echo ""
echo "🔧 Common issues diagnosis..."
echo "-----------------------------"

# Test se risponde su porta 80
if curl -f -s -m 5 http://18.171.217.18:80 >/dev/null 2>&1; then
    echo "✅ Port 80 is accessible"
else
    echo "❌ Port 80 blocked - check Security Groups"
fi

# Test se risponde su porta 8000
if curl -f -s -m 5 http://18.171.217.18:8000 >/dev/null 2>&1; then
    echo "✅ Port 8000 is accessible"
else
    echo "❌ Port 8000 blocked - check Security Groups or Docker binding"
fi

# Test HTTPS (spesso fallisce senza certificato)
echo -n "HTTPS test: "
curl -f -s -k -m 5 https://18.171.217.18 >/dev/null 2>&1 && echo "✅ OK" || echo "❌ No HTTPS (expected)"

# Riassunto finale
echo ""
echo "📝 SUMMARY"
echo "=========="

failure_count=0

# Check critico: health endpoint
if curl -f -s -m 10 http://18.171.217.18:8000/health >/dev/null 2>&1; then
    echo "✅ PRIMARY: Health endpoint working"
else
    echo "❌ PRIMARY: Health endpoint NOT working"
    failure_count=$((failure_count + 1))
fi

# Check secondario: homepage
if curl -f -s -m 10 http://18.171.217.18/ >/dev/null 2>&1; then
    echo "✅ SECONDARY: Homepage accessible"
else
    echo "❌ SECONDARY: Homepage NOT accessible"
    failure_count=$((failure_count + 1))
fi

echo ""
if [ $failure_count -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED! Your server is working correctly."
    echo ""
    echo "🔗 Ready URLs:"
    echo "   • http://18.171.217.18/"
    echo "   • http://18.171.217.18:8000/health"
    echo "   • http://18.171.217.18:8000/docs"
elif [ $failure_count -eq 1 ]; then
    echo "⚠️  PARTIAL SUCCESS: Some issues detected"
    echo ""
    echo "🔧 Suggested actions:"
    echo "   1. Check AWS Security Groups (ports 80, 8000)"
    echo "   2. Verify Docker containers: docker-compose ps"
    echo "   3. Check logs: docker-compose logs"
else
    echo "❌ MULTIPLE FAILURES: Server not accessible"
    echo ""
    echo "🚨 Required actions:"
    echo "   1. Check AWS Security Groups allow ports 80, 8000"
    echo "   2. Verify EC2 instance is running"
    echo "   3. Check Docker: docker ps"
    echo "   4. Check binding: docker-compose logs api"
fi

echo ""
echo "✅ Tests completed"