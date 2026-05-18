SIM = vcs

RTL = rtl_codes/alu.sv
TB  = rtl_codes/tb_top.sv

compile:
	$(SIM) -full64 -sverilog $(RTL) $(TB) -o simv

run:
	./simv +seed=1 +tests=100

regress:
	mkdir -p logs results waves
	@for i in 1 2 3 4 5; do \
		echo Running Seed $$i; \
		./simv +seed=$$i +tests=500 | tee logs/run_$$i.log; \
	done
